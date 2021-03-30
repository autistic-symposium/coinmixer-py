# -*- coding: utf-8 -*-
"""
jobcoin.py

Implements a class for Jobcoin API client.
"""

from __future__ import division

import sys

import jobcoin.api as api
import jobcoin.util as util


class Jobcoin(object):
    def __init__(self):
        # NOTE: We are using a "public" house address to keep track
        # of the polling on the server-side. Another option is to keep
        # it in the client-side by creating a (not ephemeral) data
        # structure that would keep track of all the balances in disk
        # or in memory, without the need for API calls.
        self.house_address = util.get_config('HOUSE_ADDRESS')

    def _is_empty(self, address):
        """Boolean test whether an address was previously seen in Jobcoin.

        Arguments:
            address (str)
        Returns:
            True if the address is empty (bool)
        """
        # NOTE: As the list of address gets larger, this method becomes
        # non-optimal. A quicker solution could be simply whether the given
        # address has balance zero (as the server API returns balance zero
        # for non-existent addresses. However, this does not guarantee that
        # the address was not used before, and it would be considered a "less
        # private" option.

        transactions = api.get_transactions()
        used_addresses = set()
        for transaction in transactions:
            used_addresses.add(transaction['toAddress'])

        if address in used_addresses:
            return False
        return True

    def validate_addresses(self, addresses):
        """Checks whether all addresses in a list are unused.

        Arguments:
            addresses_list (list of strings)
        """
        used_list = []
        for address in addresses:
            if not self._is_empty(address):
                used_list.append(address)

        if used_list:
            print('📛 Addresses need to be unused...')
            for address in used_list:
                print('📛 "{}" is not an empty address'.format(address))
            sys.exit(0)

    def _transfer_to_deposit_address(self, deposit, source_address, deposit_address):
        """Transfer coins from source address to the disposable deposit address.

        Arguments:
            deposit (str)
            source_address (str)
            deposit_address(str)
        """
        api.post_transaction(source_address, deposit_address, deposit)

    def _calculate_withdraw_value(self, deposit, personal_addresses):
        """Calculate how much each personal address receives (after fees).

        Arguments:
            deposit (str)
            personal_addresses (list of str)
        """
        withdraw_before_fee = deposit / len(personal_addresses)
        fee = int(util.get_config('FEE_PERCENTAGE'))

        if fee > 0:
            return withdraw_before_fee - withdraw_before_fee * (fee/100)
        else:
            return withdraw_before_fee

    def _run_mix_algorithm(self, deposit, deposit_address, personal_addresses):
        """Implements a simple mixer that runs small withdraws from the house
        to a list of personal addresses.

        Arguments:
            deposit (str)
            deposit_address (str)
            personal_addresses (list of str)
        """
        api.post_transaction(deposit_address, self.house_address, deposit)
        withdraw = self._calculate_withdraw_value(deposit, personal_addresses)

        max_withdraw_value = int(util.get_config('MAX_WITHDRAW_VALUE'))
        if max_withdraw_value:
            num_of_withdraw = withdraw // max_withdraw_value
            last_withdraw = withdraw % max_withdraw_value

        for address in personal_addresses:
            counter = 0
            while num_of_withdraw > counter:
                api.post_transaction(self.house_address, address, max_withdraw_value)
                counter += 1
            if last_withdraw:
                api.post_transaction(self.house_address, address, last_withdraw)

    def _print_results(self, deposit, source_address, personal_addresses):
        """Prints results at the end of the mixing.

        Arguments:
            deposit (str)
            source_address (str)
            personal_addresses (list of str)
        """
        print('✅ House withdraws {} coin(s) at time'.format(util.get_config('MAX_WITHDRAW_VALUE')))
        pretty_addresses = ', '.join(personal_addresses)
        balance_personal_addressess = api.get_balance(personal_addresses[0])
        balance_house_address = api.get_balance(util.get_config('HOUSE_ADDRESS'))

        print('✅ Successfully mixed {} coins from'.format(deposit),
              '{0} to {1}'.format(source_address, pretty_addresses))
        print('✅ Our fee is {}%, so each address'.format(util.get_config('FEE_PERCENTAGE')),
              'has now {} coin(s)\n'.format(balance_personal_addressess))
        print('🤫 House has {} coin(s)\n'.format(balance_house_address))

    def mix_algorithm(self, deposit, source_address, deposit_address, personal_addresses):
        """Entry point of this classes, selecting the mixing algorithm to be used.

        Arguments:
            deposit (str)
            source_address (str)
            personal_addresses (list of str)
        """
        deposit = util.round_float(deposit)

        self._transfer_to_deposit_address(deposit, source_address, deposit_address)

        self._run_mix_algorithm(deposit, deposit_address, personal_addresses)

        self._print_results(deposit, source_address, personal_addresses)
