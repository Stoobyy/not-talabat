elif choice == '2':
    print('Please wait while we retrieve your orders...')
    time.sleep(2)
    orders = retrieve(loginDetails)
    print('All done! Here are your orders')
    for order in orders:
        print(order)
elif choice == '3':
    print('Please wait while we retrieve your account details...')
    time.sleep(2)
    details = retrieve(loginDetails)
    print('All done! Here are your account details')
    print(f'Name: {details[1]}\nEmail: {details[0]}')
    choice = input('Would you like to change your name or email? (Enter \'n\' for no): ')
    if choice == 'n':
        pass
    else:
        choice = input('Enter your new name or email: ')
        change(loginDetails, choice)
        print('Details changed successfully')
elif choice == '4':
    print('Logging out...')
    time.sleep(2)
    print('Logged out successfully')
    exit()
else:
    print('Invalid choice')
    exit()