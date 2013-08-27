Program to test the low speed DIO cards in SuperDARN MSI radars to check for busted buffer chips.
Jumper one port of the DIO card to another port using a SCSI cable, then run the test program.

For example, to check the card with port 1 connected to port 2, run:
./dio_self_test 1 2
