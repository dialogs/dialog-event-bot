import cairosvg
import os
from config.config import config


def create_card(user):
    tmpl = config["template"]
    svg = user.name + ' ' + user.surname + '.svg'
    pdf = user.name + ' ' + user.surname + '.pdf'
    replacements = {'Name': user.name, 'Surname': user.surname, 'Company': user.org,
                    'Job Position': user.post, 'Email': user.e_mail, 'Phone': user.phone}

    with open(tmpl) as infile, open(svg, 'w') as outfile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)

    file = open(svg)
    cairosvg.svg2pdf(file_obj=file, write_to=pdf)
    file.close()
    return pdf, svg


def del_file(files):
    os.remove(files[0])
    os.remove(files[1])
