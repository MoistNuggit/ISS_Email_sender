# ISS_Email_sender

This program sends an email to you when it detects that the ISS is currenly flying overhead.
It does this by checking it's currently night time where you're located, then it uses the open-notify API to find the ISS's current location and if the ISS's locatoin is within 5 units of coordinates where you're located, it sends an email to you.
