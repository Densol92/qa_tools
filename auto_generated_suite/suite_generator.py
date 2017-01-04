from argparse import ArgumentParser

from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader

from API.TestRailAPI import TestRailAPI


def main(url, user, password, project_id, section_id):
    section, cases, author = get_sections_info(url, user, password, project_id, section_id)
    generate_module_from_template(section, cases, author)


def get_sections_info(url, user, password, project_id, section_id):
    test_rail_api = TestRailAPI(url, user, password)

    cases = test_rail_api.get_cases(project_id, section_id)
    section = test_rail_api.get_section(section_id)['name']
    author = test_rail_api.get_user(cases[0]['created_by'])

    return section, cases, author


def generate_module_from_template(test_suite_name, test_cases, author):
    env = Environment()
    env.loader = FileSystemLoader('.')
    template = env.get_template('template')
    result = template.render(test_suite_name=test_suite_name, tests=test_cases, author=author)
    result_file = open('SuiteGeneratedFromTemplate.py', 'w')
    result_file.write(result)
    result_file.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('login')
    parser.add_argument('password')
    parser.add_argument('project_id')
    parser.add_argument('section_id')
    args = parser.parse_args()
    main(args.url, args.login, args.password, args.project_id, args.section_id)
