from termcolor import cprint

from config.settings import get_proxies


def print_input_networks(chains, title='Please select network (chain)'):
    while True:
        cprint(f'{title}:', 'yellow')
        for index, chain in enumerate(chains):
            cprint(f'{index + 1}. {chain}', 'yellow')
        option_chain = int(input("> "))

        if option_chain < 1 or option_chain > len(chains) + 1:
            cprint(f'Wrong network. Please try again.\n', 'red')
            continue
        else:
            return chains[option_chain - 1]


def print_input_token():
    while True:
        cprint(f'Please select token OR write custom one:', 'yellow')
        cprint(f'1. ETH', 'yellow')
        cprint(f'2. USDT', 'yellow')
        cprint(f'3. USDC', 'yellow')
        cprint(f'4. BNB', 'yellow')
        cprint(f'5. MATIC', 'yellow')
        cprint(f'/ or write custom token symbol', 'yellow')
        option_token = input("> ")

        if option_token == '1':
            token = "ETH"
        elif option_token == '2':
            token = "USDT"
        elif option_token == '3':
            token = "USDC"
        elif option_token == '4':
            token = "BNB"
        elif option_token == '5':
            token = "MATIC"
        else:
            if 1 < len(option_token) < 5:
                token = option_token.upper()
            else:
                cprint(f'Wrong token symbol. Please try again.\n', 'red')
                continue
        return token


def print_input_sleep_sec():
    while True:
        cprint(f'Minimal sleep (5 seconds by default): ', 'yellow')
        sleep_sec = input("> ")
        try:
            if not sleep_sec:
                sleep_sec = 5
            else:
                sleep_sec = int(sleep_sec)

            if 1 <= sleep_sec <= 300:
                return sleep_sec
            else:
                cprint(f'Sleep must be between 1 and 300. Please try again.\n', 'red')
                continue
        except ValueError:
            cprint(f'Invalid number. Please try again.\n', 'red')
            continue


def print_input_transfer_amount():
    while True:
        amount = input("Withdraw amount: ")
        try:
            amount = float(amount)
            if 0.0001 <= amount <= 1000000:
                return amount
            else:
                cprint(f'Number must be between 0.0001 and 1000000. Please try again.\n', 'red')
                continue
        except ValueError:
            cprint(f'Invalid number. Please try again.\n', 'red')
            continue


def print_input_token_address(title):
    while True:
        cprint(f'{title} (or empty for ETH)', 'yellow')
        option_token = input("> ")

        if len(option_token) and len(option_token) < 42:
            cprint(f'Wrong token address. Please try again.\n', 'red')
            continue
        else:
            return option_token.lower()


def print_input_swap_amount(title):
    while True:
        cprint(f'{title} (empty for all balance)', 'yellow')
        swap_amount = input("> ")

        if not len(swap_amount):
            return 'all_balance'
        else:
            return float(swap_amount)


def get_proxy_list():
    proxies = {}
    proxy_list = get_proxies()
    if len(proxy_list) == 0:
        cprint('NOTE: No proxies in proxies.txt file.', 'blue')
    else:
        proxy = proxy_list[random.randint(0, len(proxy_list) - 1)]
        proxies = {
            'http': proxy,
            'https': proxy,
        }
    return proxies
