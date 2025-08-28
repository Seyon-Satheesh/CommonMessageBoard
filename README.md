# Common Message Board
## A very-oddly secured message board application (created for Hack Club YSWS Program Authly)

### Description:
Users can create accounts and post to a common message board where their messages are visible to all users for 24 hours. Can be used to promote local activities or programs.

### Security System:
User picks 20 random words of choosing and selects 5 of them to be their secret codes. Every time they attempt to login, they will be shown these 20 words in a randoly shuffled order and asked to identify their 5 secret ones. If chosen correctly, they will be allowed to access their account. Otherwise, they will be asked to try again (after a 250ms forced delay).

This system has 15504 potential options (20 choose 5) from which only one correct selection exists which makes this a more secure access system than a typical 4-digit PIN code. It also uses an intrinsic time delay to rate limit bot attacks which attempt to brute force into an account. The same 20 words are used for each attempt to prevent unauthorized users from deducing the correct codes after just a few attempts and they are shuffled to prevent the locations of the correct options being the same for every account.