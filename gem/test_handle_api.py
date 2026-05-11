from sequence_demo import create_demo


def mock_api(api_input: str) -> str:
    return f"MOCK_API_RESPONSE for: {api_input}"


def run_test():
    demo = create_demo()
    print(demo.next_step('Test Project'))
    print(demo.next_step('Field one'))
    print(demo.next_step('Field two'))
    # Replace API handler with mock
    demo.handle_api_step = mock_api
    print(demo.next_step('FAKE_API_PAYLOAD'))
    print('\nProgress:\n' + demo.progress())


if __name__ == '__main__':
    run_test()
