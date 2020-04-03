# Simple-WWB

## Description

This is a simple World War Bot made for fun.
It uses a set of persons that "fight" one versus one until only one is left.
Each time the game updates it randomly picks 2 persons (A, B) and a reason (R). A kills B due to R. Game updates it's state and notifies it.

## Tools used

- [AWS Lambda](https://aws.amazon.com/es/lambda/)
Is used to perform game updates and notification from time to time. [Amazon CloudWatch](https://aws.amazon.com/es/cloudwatch/) is used as a trigger that activates the lambda function in user defined intervals
- [Amazon RDS](https://aws.amazon.com/es/rds/) Is used to store the game state between calls, as Lambda being serverless cannot store data between calls.
- [Tweepy](https://www.tweepy.org/) Is used as the notifier, printing state changes in a twitter bot so that everyone can see the current status of the game

## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details