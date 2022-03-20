# eYRC-2018-Pollinator-Bee
Codes written for E-Yantra Robotics Competition 2018-19, Pollinator Bee Theme, organized by IIT Bombay.
Developed by <a href="https://github.com/nishanpoojary">Nishan Poojary</a>, <a href="https://github.com/KarlWardin27">Prathamesh Pokhare</a>, Pratik Poojary and Abhishek Pandey.

Pollinator Bee using Pluto-X drone under a program organised by IIT-Bombay. We worked on this project for 6 months under guidance of mentors from IIT Bombay.

Aim : The Drone has to imitate a bee. The drone performs a task routinely performed by bees, namely going through the process of pollinating flowers, and it is henceforth referred to as the “Pollinator Bee”. Achieved through control system design and controlling a drone using the Robot Operating System (ROS). 

<p align="center">
<img src="gifs/pollinator_bee.gif" width="350" height="250"/>
</p>

Each flower is a platform with an incomplete circuit and exposed wires. The Pollinator Bee must hover over the flower and complete the circuit. A bee stinger made of conductive material attached below the Pollinator Bee completes the circuit by causing contact between exposed terminals. LEDs on the flower light up when the contact is successful and the circuit is complete.

<p align="center">
<img src="gifs/whycon_coordinates.gif" width="350" height="250"/>
</p>

The challenge was to complete this task in the shortest time possible.

<p align="center">
<img src="gifs/image_processing.gif" width="350" height="250"/>
</p>

Thus, we needed a perfectly tuned control algorithm to make drone hold a particular position and lit the following LED Clusters.
The color of the LED clusters is detected by the Image Processing Algorithm. The control algorithm makes sure that task of pollination is performed in shortest amount of time. 

We had to complete the task assigned to us before given deadline. Some of the work done by my team is as follows :

Setting Up the Pluto-X Drone, using ROS environment, setting up Whycon camera and its calibration, writing code in Python. Also we had to setup the arena sheet (flex sheet) on which flowers is to be placed, making flowers(LED Clusters), Building Flower Structure(Stems), making Bee Stinger, building Camera Frame, etc.

Building efficient controller and Tuning PID Constants for the controller was the most challenging task as we had to tune constants considering wind speed and its ability to hold drone at a particular position correcting errors.

<p align="center">
<img src="gifs/position_hold.gif" width="350" height="250"/>
</p>

You can view the short video demonstration over <a href="https://youtu.be/BFufaY9tbUM" target="_blank" >here</a> https://youtu.be/BFufaY9tbUM 

**Tasks

*Task 1

<a href="https://www.youtube.com/watch?v=Bh3WHrjQXyo" target="_blank" rel="noopener noreferrer">Simulating the position hold of the drone at a particular point using PID controller</a>

[go](https://www.youtube.com/watch?v=Bh3WHrjQXyo){:target="_blank" rel="noopener"}


**FUNDING

The hardware kits and pluto-x drone was provided by eYantra, IIT Bombay.

