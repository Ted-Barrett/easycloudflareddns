## Installation:

Make a new directory, for example:
```
mkdir easycloudflareddns
```
Enter that directory
```
cd easycloudflareddns
```

Run the installer script:
```
curl -L https://raw.githubusercontent.com/Ted-Barrett/easycloudflareddns/main/install.sh | bash
```

## Running the program
From within the folder you created:

```
./RunEasyCloudflareDDNS.sh
```

You will likely want to set up a cron entry to automatically run the script:
```
*/15 * * * * cd <YOUR FOLDER YOU CREATED GOES HERE> && ./RunEasyCloudflareDDNS.sh
```
For example:
```
*/15 * * * * cd ~/easycloudflareddns && ./RunEasyCloudflareDDNS.sh
```

## TODO
- Update installer script to automatically setup cron
- Implement more secure access rights, for example with a dedicated user to access the install folder, so that a user who gains access to the system running the script can't steal your API key.
- Allow multiple zones to be modified (not sure if I will implement this, as you could also just provide two config files and pass them as arguments to the program separately.)
- Add screenshots to readme or somewhere else which show how to get the API key. This program is meant to be as beginner friendly as possible, so I think clear steps for every step of the way are essential.
