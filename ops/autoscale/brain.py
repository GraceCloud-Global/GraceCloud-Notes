import boto3, json, time, random
from datetime import datetime

AUTO_STATE = 'ops/autoscale/state.json'

def adjust_capacity(group_name, target_util=65):
    client = boto3.client('autoscaling')
    cpu = random.randint(30, 95)
    decision = 'stable'
    if cpu > target_util + 10:
        client.set_desired_capacity(AutoScalingGroupName=group_name, DesiredCapacity=4)
        decision = 'scale_up'
    elif cpu < target_util - 20:
        client.set_desired_capacity(AutoScalingGroupName=group_name, DesiredCapacity=2)
        decision = 'scale_down'
    record = {'timestamp': datetime.utcnow().isoformat(), 'cpu': cpu, 'decision': decision}
    json.dump(record, open(AUTO_STATE, 'w'), indent=2)
    print(f'🤖 Scaling Brain Decision: {decision} @ {cpu}%')

if __name__ == "__main__":
    adjust_capacity('gracealone-backend-asg')
