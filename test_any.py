from database.models import Agents
from domain.agent import Agent


if __name__ == '__main__':
    agent_domain = Agent(
        name = 'andre',
        team = 'bss',
        # id = 'any'
    )
    agent_model = Agents()

    for attr in agent_model._get_attrs():
        try:
            setattr(agent_model, attr, getattr(agent_domain, attr))
            print(getattr(agent_domain, attr))
        except AttributeError:
            pass

    print(agent_model.__dict__)