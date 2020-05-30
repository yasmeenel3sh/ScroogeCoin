# ScroogeCoin
Libraries needed:

pip install starkbank-ecdsa <br />
pip install pynput<br />
pip install hashlib #Notice that in python3 it is defaultly installed so this might give an error<br />


Run the Main.py file

In the main method there is a timer of 0.1 sec between each transaction creation to not overwhelm the processor

To chech double spending transaction rejection output find the word "discarded" in the Output.txt

Two type of transactions exisit:Coin creation in which srooge create one coin, Payment in which any user including scrooge can send coins to other users,
the coincreation details and scrooge sending coins to users make the initialization proces which is not shown in details to avoid overwhelming the text
file with unnecassary details.