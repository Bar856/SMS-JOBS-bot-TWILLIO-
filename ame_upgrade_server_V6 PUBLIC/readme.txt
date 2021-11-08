This project is designed for a computer that functions as a kind of "server" that always works and listens to new messages received through the TWILLIO API.
The messages are jobs that are received from a company and what the bot does is basically navigate each message to its destination without human help
The bot process:
1. Receive a message (job)
2. Transfer the message without all its details to a technician (to avoid theft of jobs)
3. The technician sends "k" + zip code or he sends pass in case and he is far or can not do the job
4. The bot sends a message to the company that we received the job
5. The technician receives the full message automatically and the job is associated with it in a csv file (in the csv folder)
6. In case the technician has a problem performing the work, he updates the bot and the message is sent to the company, and vice versa.

The cell phone addresses and numbers were censored