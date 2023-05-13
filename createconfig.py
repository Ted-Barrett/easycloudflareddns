def get_some_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value

def get_some_int(prompt, min_value, max_value):
    while True:
        value = get_some_input(prompt)
        if value.isdigit() and int(value) >= min_value and int(value) <= max_value:
            return int(value)
        else:
            print(f"Must be a number between {min_value} and {max_value}")

def get_y_n_choice(prompt, allow_empty=False):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ["y", "n"]:
            return choice == "y"
        if allow_empty:
            if not choice:
                return True

print()
with open("./LICENSE", "r") as licenceFile:
    print(licenceFile.read())

print("================================================================================")
print("=====                                                                      =====")
print("=====         Welcome to the config setup for Easy Cloudflare DDNS         =====")
print("=====           Please find above the LICENCE for this software.           =====")
print("=====                                                                      =====")
print("================================================================================")
print()

print("We will now create a config file.")
config_lines = []


key_type = 3

help_string = """
===============================================================================

To access your keys and tokens, go to dash.cloudflare.com, go to your profile
(top right menu > My Profile), and select API Tokens on the left.

There are two sections: API Tokens, and API Keys

API Keys are used to manage anything on your Cloudflare account. API Tokens can
be configured so they can only access certain properties.

(Recommended) To create an API Token:
1. Click create token
2. Click "Use template" on the "Edit zone DNS" token template
3. Make sure the permissions are set to [Zone][DNS][Edit]
4. Add your site in the Zone resources, for example:
   [Include][Specific zone][example.com]
5. Click "Continue to summary" at the bottom of the form
6. Verify the configuration and click "Create Token"
7. Copy the token

(Not recommended) To get your Global API Key
1. Click "view" in the API Keys section.
2. Enter your passord and click "View"
2. Copy the key
"""

while key_type == 3:
    print("\nYou will need a way for Easy Cloudflare DDNS to access the Cloudflare API.")
    print("Please enter the number for the option you would prefer to use:")
    print("1. Email & Global API key")
    print("2. API Token")
    print("3. Help")
    print()

    key_type = get_some_int("Choice: ", 1, 3)

    if key_type == 3:
        print(help_string)
        input("(Press enter to return to previous menu)")

if key_type == 1:
    globalkey = get_some_input("Please enter your Global API Key: ")
    config_lines.append(f"globalkey={globalkey}")

    email = get_some_input("Enter the email used for your Cloudflare account: ")
    config_lines.append(f"email={email}")
else:
    apitoken = get_some_input("Please enter your API Token: ")
    config_lines.append(f"dnskey={apitoken}")

print("\nYou will now configure which entries you wish to be updated.")
zone = get_some_input("Please enter the base domain (e.g.: example.com): ")
config_lines.append(f"root={zone}")

print("\nEnter all entries you wish to update, separated by commas.")
print("For example: example.com,www.example.com,home.example.com")
names = get_some_input("Enter your values here: ")
config_lines.append(f"names={names}")

print("\nGreat! That's all the information we need.")
print("Here is your configuration:")
print("================================================================================")
print("\n".join(config_lines))
print("================================================================================")
print("Do you wish to write these changes to cloudflare.config in the current directory?")
if get_y_n_choice("[Y(save)/n(abort and exit config creation)]", allow_empty=True):
    with open("cloudflare.config", "w") as outFile:
        outFile.writelines(line + "\n" for line in config_lines)
    print("Successfully wrote to file.")
    print("You can now run Easy Cloudflare DDNS with ./RunEasyCloudflareDDNS.sh")
    print("Goodbye!")
