"""Sample Webots controller for the square path benchmark."""
from controller import Robot
from time import sleep


class RobotMove():
    """
    This class controls a robot's movement in a square path in the Webots simulation environment.

    Attributes:
    robot (Robot): The Webots Robot object.
    rightWheel (Motor): The right wheel motor of the robot.
    leftWheel (Motor): The left wheel motor of the robot.
    leftWheelSensor (PositionSensor): The position sensor for the left wheel.
    rightWheelSensor (PositionSensor): The position sensor for the right wheel.
    """

    def __init__(self):
        """
        Initializes a new RobotMove object and sets up the robot's components and initial velocities.
        """
        self.robot = Robot()
        self.rightWheel = self.robot.getMotor('right wheel')
        self.leftWheel = self.robot.getMotor('left wheel')
        self.leftWheelSensor = self.robot.getPositionSensor('left wheel sensor')
        self.rightWheelSensor = self.robot.getPositionSensor('right wheel sensor')
        
        # Refreshes the sensor every 1ms.
        self.rightWheelSensor.enable(1)
        self.leftWheelSensor.enable(1)
        
        self.rightWheel.setVelocity(5.2)
        self.leftWheel.setVelocity(5.2)
        
    def square(self):
        """
        Makes the robot move in a square path by calling other methods for each step.

        The square path consists of four straight segments and four right turns.

        The speed of the robot can be controlled depending on the current supplied to the motors. So both wheels can
        have different speeds the same time. robot.step() controls the number of steps taken by the robot, however the
        number of steps can also vary depending on  wheel speeds. By default, each square is 1000 steps of the robot,
        the number of wheel revolutions will always be 20 (right) ~ 23 (left) regardless from the speed of the robot,
        which comes out to ~ 5 revolutions per square.

        """
        for i in range(0, 4):
            if i == 0:
                self.move_forward(250)
                # Then, set the right wheel backward, so the robot will turn right.
                print(self.rightWheelSensor.getValue() - self.leftWheelSensor.getValue())
                print("check")
                
                print(self.rightWheelSensor.getValue())
                print(self.leftWheelSensor.getValue())
               
                self.turn_right(480)
               
            if i == 1:
                # adjusting wheels every square
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(57)
                 
                self.turn_right(480)
             
            if i == 2:
                
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(63)
                self.adjust_wheels(-1.45, 1.45)
                self.move_forward(63)
               
                self.turn_right(480)
            
            if i == 3:
                 
                self.move_forward(250)

    def move_forward(self, limit):
        """
        Makes the robot move forward for a specified number of steps.

        Each step is equal to one so that the robot does not fly out of its path at high speed

        Parameters:
        limit (int): The number of steps to move forward.
        """
        steps = 0

        self.leftWheel.setPosition(1000)
        self.rightWheel.setPosition(1000)
        
        # defines how many steps we do
        # limit - 250 (full line)
        while (steps < limit):
            self.robot.step(1)
            steps += 1
        
    def turn_right(self, steps):
        """
        Makes the robot turn right by setting the wheel velocities. 1000 (left wheel) value means that wheel faces forward, -1000 (rigth wheel) faces backward.

        Parameters:
        steps (int): The number of simulation steps for the right turn.
        """
        # right wheel faces backwards| left forwards
        self.leftWheel.setPosition(1000)
        self.rightWheel.setPosition(-1000)
        
        self.robot.step(steps)

    def stop(self):
        """
        Stops the robot by setting both wheel velocities to 0.
        """
        self.leftWheel.setVelocity(0)
        self.rightWheel.setVelocity(0)
        
    def adjust_wheels(self, neg_value, pos_value):
        """
        Parameters:
        is_right (bool): To check which wheel moves faster to stop it for a some period of time and then turn it back on
        self.rightWheelSensor.getValue() (str): Gets the number of revolutions of the right wheel using the right sensor every 1 ms
        self.leftWheelSensor.getValue() (str): Gets the number of revolutions of the left wheel using the left sensor every 1 ms
        negValue (float): The negative threshold for the sensor difference.
        posValue (float): The positive threshold for the sensor difference.

        The left wheel moves faster by default, ~5.8 revolutions faster starting from the second line of the square, that is, 1.45 revolutions each
        I square a cell. Based on this data, we adjust the position of the robot every cell of the square, turning off the left or right wheel by
        time until the robot takes from 7 to 15 steps (half a square or a whole square)
        """
        is_right = False
        if (self.rightWheelSensor.getValue() - self.leftWheelSensor.getValue() < neg_value):
            self.leftWheel.setVelocity(0)
            # half a square
            self.robot.step(7)
            is_right = True
        elif (self.rightWheelSensor.getValue() - self.leftWheelSensor.getValue() > pos_value):
            self.rightWheel.setVelocity(0)
            self.robot.step(7)

        if is_right:
            self.leftWheel.setVelocity(5.2)
        else:
            self.rightWheel.setVelocity(5.2)
    

robott = RobotMove()
robott.square()
robott.stop()
