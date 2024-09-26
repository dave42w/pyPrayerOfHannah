# pyPrayerOfHannah

Free Software to provide Slides as a web service for Worship, Noticeboards and more.

Named in honour of Hannah (see 1 Samuel 2:1-10) and particularly from verse 8:
"He raises up the poor from the dust;
he lifts the needy from the ash heap"

pyPrayerOfHannah is a python replacement for the original project PrayertOfHannah which I started using Rust. Switching to Python in part duie to the quality of the SQL ecosystem in Rust.

## Purpose

There are many software options for projecting Worship or presentation slides or noticeboard slides.

However, PrayerOfHannah is going to be unique:

- access from anywhere with a Internet connection (even a slow mobile hot-spot). This will allow services to be prepared by multiple people, in different locations with no issues about extra licenses, extra installations, setting up DropBox or anything else. It will allow satellite sites (fom individuals at home to whole venues), again without specialized equipment.
- Fantastic support for accessibility as people can have a tablet with them allowing both huge text (right close to them adjustable for angle brightness etc) and sound direct into headphones/hearing aid by wire or bluetooth
- support is so much easier, if you are struggling with a service or with data then you can allow someone direct access to your data.

## More details

- Internet Server based model with multiple Web Browser Clients
- Free Software under The GNU Affero General Public License that means if someone offers you the application as an Internet service they have to give you the version of the code they are using.
- Hosting will be available from Dave Warnock (the original designer). However, any other server can host PrayerOfHannah
- You can self-host on either your LAN (if you want a high speed setup with lots of video, sound and displays) or the Internet for zero cost

## Features

### Multiple Slide Types

Initially we will start with Songs with blank slide dividers. Then we will be adding

- Custom Slides (initial focus is Liturgy)
- Images

We will allow import of multiple songs allowing you to load whole hymn books. The schema will allow multiple versions of a song (no audio, pre-recorded audio, different words to match different audio, video). An easy way to miss out verses or change the order for a particular service.

### Multiple Client Views

We don't think anyone else is doing this (at least not from a single server application):

- (1st Priority) standard projection view for any Screen or Projector with an attached device with a web browser (cheapest option will often be a single-board computer such as a Raspberry Pi attached directly to the display using WiFi so no expensive Data cabling or Data transmitters/receivers)
- standard projection view for any Screen or Projector with builtin web browser
- Pew views. Particularly helpful for anyone who is partially sighted. Display the same projection view onto a tablet that they hold or is attached to a convenient stand. Follows the service without needing any interaction. So much more visible and never looses their place.
- (2nd Priority) controller view. A basic "remote" for a mobile phone
- multiple controller views. More sophisticated view with more controls and a service item list Have as many live as you need. For example the preacher, the band, the sound desk could all have live controller views on phones, tablets or computers. This will allow any of them to move to next slide or around the service. Typically the preacher might want control when preaching but not when presiding at Holy Communion. For songs the band leader can use a foot pedal or the sound desk could control it for them allowing flexibility in jumping around the verses/chorus/bridges.
- remote worshippers. As the service can be run from a server on the Internet it is possible to for anyone (with appropriate authentication if desired) to be able to watch the service slides
- a variation of the views to suit more generic presentations
- an automated slide view suitable for noticeboards. To save buying, learning and managing a separate solution. This way the digital noticeboard can be switched to show the live worship view when as it happens.

### Input options

Bandwidth permitting we will be able to receive multiple input sources that stream sound or video to the server. One input might be from the sound desk of whatever the current mix is. Another could be a remote person doing a reading, or being interviewed. Another could be video either live or recorded. Again you can use single-board computers with a microphone and wifi connection to get the sound in.

### Sound output options

- sound from the server can be sent to a sound desk "view" to connect to the hearing aid loop or speakers
- remote worshipers can hear the same sound
- Pew views. For the hard of hearing could directly connect headphones or a hearing aid
- extension worship spaces, creche etc can all have the sound on

## Display Technique

We will use a standard web browser that is set to fill the screen on a phone or tablet and follow normal sizing control on laptops and PC's but with the option to automatically start in "kiosk" mode for projectors etc.

## The Tech stuff

PrayerOfHannah is written in Python, and uses HTMx to enhance the user experience. The data is stored in Sqlite.

## Supporting PrayerOfHannah

PrayerOfHannah is guaranteed to always be free software. The license ensures that nobody can offer an upgraded/customized version without making the code available for free so that you can host it yourself or elsewhere.

Following the spirit of Hannah: 1 Samuel 2:8:
"He raises up the poor from the dust;
   he lifts the needy from the ash heap"
my plan is to fund the development and hosting of PrayerOfHannah via donations, where my intention is that if you have money you pay so that others can use this, including hosting, for free. There should be no fixed hosting fee, you pay what you can afford, knowing how much it costs us. The only exception is that Churches and others in areas of deprivation, wherever they are in the world, should pay nothing. Those in wealthy places should not consider this a cheap option, you role is to be alongside God raising the poor.

At present you can support the development and hosting of PrayerOfHannah using [Ko-Fi](https://ko-fi.com/prayerofhannah) they don't charge us anything, all we pay is the PayPal processing fee (later we will be moving to Ko-Fi processing with Stripe for lower fees). We welcome one off and regular donations of any amount.
#
## Import song format

This is a slightly simplified version of the xml format used by OpenLP (find and replace to take out a lot of structure in the verses that we don't need)
