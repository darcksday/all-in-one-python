from libs.binance import binance_withdraw
from libs.bridges import orbiter_bridge
from libs.console_helpers import *
from libs.debank import *
from termcolor import cprint
from libs.swap import swaps
from libs.transfers import transfer


def inner_check_balance():
    cprint(f'Checking balances...', 'yellow')

    # баланс монет выше этого числа в $ эквиваленте будут записаны в таблицу,
    # если меньше, то только в total value
    min_table_amount = 1
    func = [
        'protocols',
        'tokens',
        # 'nfts'
    ]
    checker_main(func, min_table_amount)


def inner_swap():
    private_keys = get_private_keys()
    if not len(private_keys):
        cprint(f'\nError: No private keys in private_keys.txt file', 'red')
        return

    network = print_input_networks(['ETH', 'OPTIMISM', 'BNB', 'MATIC', 'FTM', 'ARBITRUM', 'AVAXC'])
    from_token_address = print_input_token_address('From token address')
    to_token_address = print_input_token_address('To token address')
    amount_to_swap = print_input_swap_amount('Amount to swap')

    # AMOUNT_TO_SWAP = round(random.uniform(25, 30), 0) # от 1 до 3, 5 цифр после точки
    # MIN_BALANCE = round(random.uniform(0.005, 0.01), 5) # останется FROM_TOKEN на балансе после свапа
    min_balance = 0  # останется FROM_TOKEN на балансе после свапа
    min_amount = 0  # если AMOUNT_TO_SWAP меньше этого числа, тогда не свапаем
    for private_key in private_keys:
        swaps(
            private_key,
            network,
            from_token_address,
            to_token_address,
            amount_to_swap,
            min_balance,
            min_amount
        )


def inner_bridge():
    private_keys = get_private_keys()
    if not len(private_keys):
        cprint(f'\nError: No private keys in private_keys.txt file', 'red')
        return

    from_chain = print_input_networks(
        ['ETH', 'OPTIMISM', 'BNB', 'ARBITRUM', 'NOVA', 'MATIC', 'ZKSYNC LITE', 'ZKSYNC ERA', 'STARKNET', 'ZKEVM'],
        'FROM Chain'
    )
    to_chain = print_input_networks(
        ['ETH', 'OPTIMISM', 'BNB', 'ARBITRUM', 'NOVA', 'MATIC', 'ZKSYNC LITE', 'ZKSYNC ERA', 'STARKNET', 'ZKEVM'],
        'TO Chain'
    )
    amount_to_bridge = print_input_swap_amount('Amount to bridge')
    sleep_sec = print_input_sleep_sec()

    # AMOUNT_TO_BRIDGE = 'all_balance'
    # AMOUNT_TO_BRIDGE = round(random.uniform(0.03, 0.04), 6)
    # AMOUNT_TO_BRIDGE = 10
    min_balance = 0  # останется токенов на балансе после бриджа
    for private_key in private_keys:
        orbiter_bridge(private_key, from_chain, to_chain, amount_to_bridge, min_balance)
        sleeping(sleep_sec, sleep_sec + 10)


def inner_transfer():
    private_keys = get_private_keys()
    recepients = get_recipients()

    if not len(private_keys):
        cprint(f'\nError: No private keys in private_keys.txt file', 'red')
        return
    if len(private_keys) != len(recepients):
        cprint(f'\nError: Wrong amount of recipients, check private_keys.txt and recipients.txt files', 'red')
        return

    network = print_input_networks(
        ['ETH', 'OPTIMISM', 'BNB', 'ARBITRUM', 'NOVA', 'ZKSYNC ERA', 'MATIC', 'FTM', 'AVAXC', 'ZKEVM'],
        'Select Network'
    )
    token_address = print_input_token_address('Token address')
    amount_to_transfer = print_input_swap_amount('Amount to transfer')
    sleep_sec = print_input_sleep_sec()

    MIN_BALANCE = round(random.uniform(0.012, 0.015), 6)  # останется токенов на балансе после бриджа
    MIN_AMOUNT = 0.005  # если AMOUNT_TO_TRANSFER меньше этого числа, тогда не выводим

    for index, private_key in enumerate(private_keys):
        to_address = recepients[index]
        transfer(private_key, to_address, network, amount_to_transfer, token_address, MIN_BALANCE, MIN_AMOUNT)
        sleeping(sleep_sec, sleep_sec + 10)


def inner_binance():
    wallet_list = get_wallet_list()
    if not len(wallet_list):
        cprint(f'\nError: No wallets in wallet_list.txt file', 'red')
        return

    network = print_input_networks(['ETH', 'BSC', 'AVAXC', 'MATIC', 'ARBITRUM', 'OPTIMISM', 'APT'])
    token = print_input_token()
    amount = print_input_transfer_amount()
    sleep_sec = print_input_sleep_sec()

    # amm = random.randint(2, 6)
    # amount_to_withdraw = round(random.uniform(0.02, 0.03), amm)
    cprint(f'Withdraw {amount} {token} using {network} chain for {len(wallet_list)} wallets.', 'blue')
    cprint(f'TOTAL: {len(wallet_list) * amount} {token}.\n', 'blue')
    approval = input("Do you approve of this result? (y/N): ")
    if approval.lower() != "y":
        cprint(f'Action Canceled.\n', 'red')
        return

    for wallet_address in wallet_list:
        binance_withdraw(
            wallet_address,
            amount,  # amount to withdraw
            token,  # token symbol to withdraw
            network  # network
        )
        sleeping(sleep_sec, sleep_sec + 10)





if __name__ == "__main__":
    try:
        while True:
            cprint(f'Please select an action:', 'yellow')
            cprint(f'1. Check Balances', 'yellow')
            cprint(f'2. Swap Tokens', 'yellow')
            cprint(f'3. Bridge Tokens', 'yellow')
            cprint(f'4. Transfer Tokens', 'yellow')
            cprint(f'5. Binance Withdraw', 'yellow')
            cprint(f'0. Exit', 'yellow')
            option = input("> ")

            if option == '0':
                cprint(f'Exit, bye bye.', 'green')
                break
            elif option == '1':
                inner_check_balance()
                break
            elif option == '2':
                inner_swap()
                break
            elif option == '3':
                inner_bridge()
                break
            elif option == '4':
                inner_transfer()
                break
            elif option == '5':
                inner_binance()
                break

            else:
                cprint(f'Wrong action. Please try again.\n', 'red')
                continue

    except KeyboardInterrupt:
        cprint(f' Exit, bye bye\n', 'red')
        raise SystemExit
