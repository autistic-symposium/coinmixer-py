#!/usr/bin/env python
"""
cli.py

CLI entry point for Jobcoin app.
"""

import sys
import click

import jobcoin.util as util
from jobcoin.jobcoin import Jobcoin


@click.command()
def main(args=None):

    client = Jobcoin()

    print('✨ Welcome to the Jobcoin mixer! ✨\n')

    while True:
        addresses = click.prompt(
            'Please enter a comma-separated list of new, unused Jobcoin '
            'addresses where your mixed Jobcoins will be sent.',
            prompt_suffix='\n[blank to quit] > ',
            default='',
            show_default=False)

        # Validate list of addresses
        personal_addresses = util.get_addresses_list(addresses)
        client.validate_addresses(personal_addresses)

        # Generate a deposit address
        deposit_address = util.generate_deposit_address()
        click.echo(
            '\n✅ You may now send Jobcoins to address {deposit_address}. '
            'They will be mixed and sent to your destination addresses.'
            .format(deposit_address=deposit_address))

        # Get source address
        source_address = click.prompt(
            '\nPlease enter the (source) address. ',
            prompt_suffix='\n[source address] > ',
            default='',
            show_default=False)

        # Get number of coins to be deposited
        deposit = click.prompt(
            '\nPlease enter the value to be transferred.',
            prompt_suffix='\n[deposit value] > ',
            default='',
            show_default=False)

        # Run mix algorithm
        print('\n✅ Starting Jobcoin Mixer algorithm')
        client.mix_algorithm(deposit,
                             source_address,
                             deposit_address,
                             personal_addresses)


if __name__ == '__main__':
    sys.exit(main())
