from io import StringIO
from subprocess import run, PIPE
from flask import render_template, flash

generate_view = 'generate.html'


def check_numerical_parameters(form, bash_script, flash_func, numerical):
    """
    Checks the numerical parameters
    :param form: dictionary of the request form
    :param bash_script: script to insert values into
    :param flash_func: function to flash the client with
    :param numerical: numerical parameters with names and values

    :return bash_script: the edited script
    :return found_false_input: if any false input was found
   """
    found_false_input = False
    for numerical_param in numerical:
        if form[numerical_param[1]].isnumeric():
            bash_script += f"--{numerical_param[1]}={form[numerical_param[1]]} "
        elif form[numerical_param[1]] != '':
            flash_func(f'{numerical_param[0]} must be a number', numerical_param[1])
            found_false_input = True
    return bash_script, found_false_input


def check_switches(form, bash_script, flash_func, switches):
    """
    Checks the switch parameters.
    :param form: dictionary of the request form
    :param bash_script: script to insert values into
    :param flash_func: function to flash the client with
    :param switches: switch parameters with names and values

    :return bash_script: the edited script
    :return found_false_input: if two or more switches were active
   """
    found_input, found_false_input = False, False
    for switch_param in switches:
        if form.get(switch_param[1]) is not None:
            if not found_input:
                bash_script += f"--{switch_param[1]} 1 "
                found_input = True
            else:
                found_false_input = True
    if found_false_input:
        flash_func('Only one switch may be active', 'switch')
    return bash_script, found_false_input


def get_time_data(stdout):
    """
    Parse the arguments.
    :param stdout: output of the bash script
    :return: time data.
    """
    time_data = {}
    for line in StringIO(stdout):
        if 'Total Time: ' in line:
            time_data['Total time'] = float(line.split(' ')[2][:-2])
        elif 'Object Creation Time: ' in line:
            time_data['Object creation'] = float(line.split(' ')[3][:-2])
        elif 'Object Setup Time: ' in line:
            time_data['Object setup'] = float(line.split(' ')[3][:-2])
        elif 'Image ' in line and ' Time: ' in line:
            time_data['Image ' + line.split(' ')[1]] = float(line.split(' ')[3][:-2])
    return time_data


def generate_images(form, material_list, material_prop, configuration):
    """
    Parse the arguments and run the bash script
    :param form: dictionary of the request form
    :param material_list: list of materials to insert
    :param material_prop: list of proportions to insert
    :param configuration: configuration of the server

    :return: either download or generate view depending on the input
    """
    bash_script = 'docker run -it --rm -v "$(pwd)":/workdir ' \
                  'recycleye blender -noaudio -b -E CYCLES -P src/blender/main.py -- ' \
                  f'-m {material_list} ' + f'-p {material_prop} '
    bash_script, found_false_input = \
        check_numerical_parameters(form, bash_script, flash, configuration['numerical'])
    bash_script, found_false_input_2 = \
        check_switches(form, bash_script, flash, configuration['switches'])
    if found_false_input or found_false_input_2:
        return render_template(generate_view, configuration=configuration, form=form)
    completed_process = run(bash_script, shell=True, stdout=PIPE, encoding="utf-8")
    print(completed_process.stdout)
    time_data = get_time_data(completed_process.stdout)
    return render_template('download.html', time_data=time_data)


def check_materials(form, materials, flash_func):
    """
    Checks the material proportions.
    :param form: dictionary of the request form
    :param materials: list of material names
    :param flash_func: function to flash the client with

    :return material_list: list of materials for the bash script
    :return material_prop: list of proportions that were checked to be numeric
    :return total_prop: total proportion that was calculated
    :return found_false_input: if any false input was found
    """
    material_list = ""
    material_prop = ""
    total_prop = 0
    found_false_input = False
    for material in materials:
        if form[material].isnumeric():
            material_list += material + ' '
            material_prop += form[material] + ' '
            total_prop += int(form[material])
        elif form[material] != '':
            flash_func('The proportion must be a number', material)
            found_false_input = True
    return material_list, material_prop, found_false_input, total_prop


def check_generate(form, configuration):
    """
    Checks the generate form.
    :param form : dictionary of the request form
    :param configuration: configuration of the server
    """
    material_list, material_prop, found_bad_input, total_prop \
        = check_materials(form, configuration['materials'], flash)
    if found_bad_input:
        return render_template(generate_view, configuration=configuration, form=form)

    if total_prop != 100:
        flash('The proportion must add up to 100', 'error')
        return render_template(generate_view, configuration=configuration, form=form)
    else:
        return generate_images(form, material_list, material_prop, configuration)
