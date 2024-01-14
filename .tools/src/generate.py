import json
import jinja2
import os

# Create a Jinja2 environment
env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)


# This method builds a list of resources and their entries
def generate_resource_and_entry_list(config):
    resources = []

    print(f"Data directory: {config['data_dir']}")
    print(f"Generating resource and entry list...")

    for resource in config["resources"]:
        resource_file = f"{config['data_dir']}/{resource['ref']}.json"

        print()
        print(f"Resource file: {resource_file}")

        try:
            with open(resource_file, "r") as file:
                try:
                    resource_data = json.load(file)
                    entries = []

                    for entry in sorted(resource_data, key=lambda x: x["name"]):
                        entries.append(entry)

                    resource.update({"entries": entries})

                    resources.append((resource))
                except json.JSONDecodeError as e:
                    print()
                    print(
                        f"Error decoding JSON in resource file '{resource_file}' at line {e.lineno}: {e.msg}"
                    )
                    print()
                    exit(1)
        except FileNotFoundError:
            print(f"Warning: Resource file '{resource_file}' not found. Skipping...")
            continue

    # print(json.dumps(resources, indent=4))

    return resources


def load_template(template_file):
    try:
        with open(template_file, "r") as file:
            return env.from_string(file.read())

    except FileNotFoundError:
        print(f"Warning: Template file '{template_file}' not found. Skipping...")
        return


def generate_header(config):
    header_template = f"{config['templates_dir']}/header.md.jinja"

    try:
        with open(header_template, "r") as file:
            header_template = env.from_string(file.read())

    except FileNotFoundError:
        print(f"Warning: Template file '{header_template}' not found. Skipping...")
        return

    return header_template.render(config)


def generate_footer(config):
    footer_template = f"{config['templates_dir']}/footer.md.jinja"

    try:
        with open(footer_template, "r") as file:
            footer_template = env.from_string(file.read())

    except FileNotFoundError:
        print(f"Warning: Template file '{footer_template}' not found. Skipping...")
        return

    return footer_template.render(config)


def main():
    # Read the configuration file
    with open("config.json", "r") as file:
        config = json.load(file)

    # Initialize README content
    readme_content = generate_header(config) + "\n\n"

    # Add resource and entry list
    resources = generate_resource_and_entry_list(config)

    # Print resources & exit
    print("=========================")
    print("=== Table Of Contents ===")
    print("=========================")
    print()

    table_of_contents_template = load_template(
        f"{config['templates_dir']}/table-of-contents.md.jinja"
    )

    readme_content += table_of_contents_template.render(resources=resources) + "\n\n"

    print("=================")
    print("=== Resources ===")
    print("=================")

    resource_header_template = load_template(
        f"{config['templates_dir']}/resource_header.md.jinja"
    )
    resource_footer_template = load_template(
        f"{config['templates_dir']}/resource_footer.md.jinja"
    )

    # Process each resource entry
    for resource in resources:
        print()
        print(f"=== Processing resource '{resource['name']}'... ===")
        print()
        print(f"=== Generating resource header ===")
        print()

        readme_content += resource_header_template.render(resource) + "\n"

        print(f"=== Generating resource '{resource['name']}'... ===")
        print()

        resource_template = load_template(
            f"{config['templates_dir']}/resources/{resource['ref']}.md.jinja"
        )

        # print(json.dumps(resource["entries"], indent=4))

        for entry in resource["entries"]:
            print(f"Entry: {entry['name']}")
            readme_content += (
                resource_template.render(entry, resource=resource) + "\n\n"
            )

        readme_content += resource_footer_template.render() + "\n\n"

    print()

    print("=================")
    print("=== Footer... ===")
    print("=================")

    readme_content += generate_footer(config)

    # Write to README.md
    with open("dist/README.md", "w") as md_file:
        md_file.write(readme_content)

    print()

    print("README.md file generated successfully.")


if __name__ == "__main__":
    main()
