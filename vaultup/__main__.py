"""
Main entry-point for vaultup.

Parses arguments from the CLI, and performs the action.
"""

if __name__ == '__main__':
    from vaultup import cli

    ns = cli.parser.parse_args()
    action = cli.actions[ns.action]
    action.parse(ns)

    print(action.__dict__)
    # TODO: Execute the action
