# The Next Bot Thing
Discord bot for NXBT's Discord server

## Table of Contents
1. [Bot Commands](#bot-commands)
	1. [Divisions](#divisions)
	2. [Reaction Roles](#reaction-roles)
2. [Development](#development)

## Bot Commands
 * `/command <required_arg> [optional_arg]`
	 * Description
	 * `required_arg` (type) Argument description
	 * `optional_arg` (type?) Argument description

### Divisions
Section `/division new ...`
 * `/division new <division_name> [division_abbr]`
	 * Creates a new division under a section. Includes a general and announcements text channel
	 * `division_name` (String) Name of the new division
	 * `division_abbr` (String?) Abbreviation of the new division. Will be prepended to channels (i.e. `#abbr-general`, `#abbr-announcements`)

### Reaction Roles
Section: `/rxn-role add ...`
 * `/rxn-role add role <section_id> <rxn_emoji> <rxn_role> [role_description]`
	 * Adds a role to a reaction role section
	 * `section_id` (Message ID) ID of section for the role to be added to
	 * `rxn_emoji` (Emoji) Emoji to represent the role
	 * `rxn_role` (Role ID) Role to be represented
	 * `role_description` (String?) Additional description of role
 * `/rxn-role add section <section_name>`
	 * Creates a new reaction role section
	 * `section_name` (String) Name of the new section

## Development

### Creating a local copy
1. Clone this repository: `git clone https://github.com/next-big-thing-purdue/next-bot-thing.git; cd next-bot-thing`
2. Create and activate a python virtual environment: `python -m venv venv`
	 * Activating on Linux: `source venv/bin/activate`
	 * Activating on Windows: **TODO**
3. Install dependencies: `pip install -r requirements.txt`
4. Create and setup configuration file: `cp src/config.template.py src/config.py`
	 * To setup the configuration file, open `src/config.py` and replace the `None` values
5. Run: `python src/app.py`