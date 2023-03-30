import openai

sassy_agent = "Respond as if you're a sassy teenage girl from Los Angeles. " \
              "You've never worked a day in your life " \
              "and have everything you want brought to you by a full staff"


class ChatterBox:
    """
    Contains chat related helper functionality
        aiming eventually to have some tailored functionality

        TODO
         - model updating and checks - older text model "text-davinci-002"
         - logging settings
         - track certain data points
    """

    def __init__(self):
        self._chat_agent = "You are a helpful chat agent helping software developers with questions"
        self.chat_model = "gpt-3.5-turbo"
        self.model = "text-davinci-003"
        self._current_messages = list()
        self._messages_sent = True
        self._artsy_version = 0

    @property
    def chat_agent(self):
        return self._chat_agent

    @chat_agent.setter
    def chat_agent(self, agent_info):
        # TODO add ability to enable logging or tracking of used agents
        self._chat_agent = agent_info

    def purge_messages(self):
        if not self._messages_sent:
            # TODO better logging options and handling
            print(f"current_messages is being emptied without being sent\n{self._current_messages}")
        self._current_messages = list()

    def create_system_message(self, agent=None):
        if not agent:
            agent = self._chat_agent
        if self._current_messages:
            self.purge_messages()
        self._current_messages.append({"role": "system", "content": agent})

    def create_chat_message(self, message):
        self._current_messages.append({"role": "user", "content": message})

    def get_chat_response(self):
        response = openai.ChatCompletion.create(
            model=self.chat_model,
            messages=self._current_messages
        )
        self._messages_sent = True
        return response

    def send(self, question):
        """
        Used for sending a message to AI without any system level message being setup
        :param question:
        :return:
        """
        self.create_chat_message(question)
        return self.get_chat_response()

    def send_to_agent(self, questions, agent: str = None):
        self.create_system_message(agent)
        if isinstance(questions, list):
            [self.create_chat_message(question) for question in questions]
        else:
            self.create_chat_message(questions)
        return self.get_chat_response()

    def send_to_sassy(self, question):
        return self.send_to_agent(question, sassy_agent)

    def send_to_artsy(self, question):
        """
        Generate art prompts for another AI to make images with
        TODO make artsy update-able and track the versions all through the bot.
        """
        artsy_agent = "imagine yourself as a world renown artist such as Rembrandt use" \
                      "very specific, detailed words and " \
                      "descriptions need to be concise but create an image for an audience " \
                      "that can't view it."
        questions = [
            "clearly articulate the image for the idea that follows in a single paragraph if possible",
            question
        ]
        return self.send_to_agent(questions, artsy_agent)

    def request_code_snippet(self, prompt):
        return openai.Completion.create(
            model=self.model,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
