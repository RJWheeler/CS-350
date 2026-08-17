# CS 350 Module Eight Journal

## Project Artifacts

The two artifacts I selected from this course are my **Milestone Three Morse Code project** and my **Final Thermostat project**. I chose these projects because they demonstrate my progression in working with embedded systems and hardware interfaces. The Milestone Three project demonstrates my ability to use a state machine, LEDs, buttons, and an LCD to create a Morse code communication system. The Final Thermostat project expanded on those skills by incorporating a temperature and humidity sensor, PWM LEDs, multiple buttons, an LCD display, I2C communication, and UART communication.

## Summarize the project and what problem it was solving.

The final project involved creating a prototype smart thermostat using a Raspberry Pi 4B. The purpose of the project was to demonstrate the basic functionality that could eventually be used in a commercial smart thermostat. The thermostat used an AHT20 temperature sensor to determine the current room temperature and allowed the user to select between off, heating, and cooling states. The red and blue LEDs indicated whether the system was heating or cooling, while the LCD displayed information about the thermostat. Buttons allowed the user to change the thermostat state and increase or decrease the temperature set point. UART was also used to simulate sending thermostat information to a server.

The Milestone Three project focused on using a state machine to control red and blue LEDs to communicate Morse code messages. A button allowed the user to switch between messages. This project helped establish the state-machine concepts and GPIO programming that were later used in the thermostat project.

## What did you do particularly well?

I think I did particularly well with integrating the different hardware components into a single working system. The final project required several different technologies to work together, including GPIO, PWM, I2C, UART, buttons, LEDs, an LCD, and a state machine. I was able to build on the previous milestones instead of treating each component as a completely separate project.

I also did well with troubleshooting. Throughout the course, I encountered problems involving wiring, software, GPIO configuration, and communication between the Raspberry Pi and hardware components. Working through these issues helped me become more comfortable reading error messages and testing individual components to determine where a problem was occurring.

## Where could you improve?

One area where I could improve is planning and troubleshooting hardware connections before beginning the software portion of a project. Hardware problems can be difficult to identify because a component can appear to have power while still not communicating correctly with the Raspberry Pi. I could also improve by documenting wiring and pin assignments more thoroughly as I build the circuit. This would make troubleshooting easier and reduce the possibility of accidentally using the wrong GPIO connection.

I could also improve my experience with embedded Linux and hardware debugging tools. While I became more comfortable with the Raspberry Pi during this course, there are still areas of hardware troubleshooting and communication protocols that I would like to understand at a deeper level.

## What tools and/or resources are you adding to your support network?

This course introduced me to several tools and resources that I can continue using in future projects. Raspberry Pi documentation, GPIOZero, Adafruit libraries, Python documentation, I2C tools, and pinout diagrams are all useful resources for embedded systems development. I also became more comfortable using a Linux terminal and working with Python directly on a Raspberry Pi.

GitHub is another important resource because it provides a way to store, organize, and present my projects. Maintaining a portfolio of working projects will give me something concrete to show potential employers when discussing my software and embedded systems experience.

## What skills from this project will be particularly transferable to other projects and/or coursework?

The most transferable skills are Python programming, state-machine design, GPIO programming, debugging, working with sensors, and integrating multiple hardware and software components. Understanding how hardware communicates with software through interfaces such as I2C and UART will also be useful in future embedded systems projects.

The troubleshooting skills I developed are particularly transferable. Not every technical problem has an obvious solution, so being able to isolate a problem, test individual components, examine error messages, and make changes one at a time will be useful in both software development and hardware projects.

## How did you make this project maintainable, readable, and adaptable?

I made the project more maintainable by separating different responsibilities within the program. The state machine was responsible for controlling the thermostat states, while separate methods handled temperature readings, display updates, serial output, button events, and LED behavior. Comments were also included throughout the code to explain the purpose of different sections and hardware connections.

The use of variables such as the thermostat set point and separate methods for updating the lights and display also makes the program easier to modify. For example, the set point can be changed without having to rewrite the state machine. The project could also be expanded in the future to support additional sensors, different thermostat settings, or actual Wi-Fi communication with a server.

## Reflection

This course gave me practical experience with embedded systems that went beyond writing software that runs entirely on a computer. I had to consider how software interacts with physical hardware and how different components communicate with one another. The projects also showed me how important testing and troubleshooting are when developing an embedded system.

The final thermostat project was especially valuable because it combined many of the concepts from the course into one system. I can use this project in my portfolio to demonstrate that I have experience developing interface software, working with hardware peripherals, designing state-machine logic, and troubleshooting an embedded system.
