import random

# lists for the chatbot-functions
verbs = ["eat", "study", "play", "code", "work", "think", "sleep", "read", "fly", "talk", "laugh", "climb"]
alternatives = ["stealing", "leaving", "loitering"]
likes = ["climb", "laugh", "talk", "fly"]
meh = ["sleep", "read", "think", "work"]
dislikes = ["eat", "study", "play", "code"]
alternatives_all = ["drink", "lie", "beat", "leave", "talk",
                "eat", "sleep", "cry", "complain", "fight", "yell"]
bad_verbs = ["fighting", "yelling", "beating", "drinking", "leaving", "crying"]
hard_things = ["regex", "to traverse a linked list", "bash-scripting"]
all_list = []
alexa_list = []
siri_list = []
siri_likes = ["watch youtube", "watch tiktok", "watch netflix", "watch HBO", "look at memes"]
cortana_list = []
watson_list = []


# finds the verb in the suggested action
def extract_verb(suggestion):
    for verb in verbs:
        if verb in suggestion:
            return verb


# sends response
def chatbot_response(bot, verb, alternative_verb=None):
    if bot == "watson":
        return watson(verb, alternative_verb)
    if bot == "siri":
        return siri(verb, alternative_verb)
    if bot == "cortana":
        return cortana(verb, alternative_verb)
    if bot == "alexa":
        return alexa(verb, alternative_verb)
    if bot == "all":
        return all_chatbots(verb, alternative_verb)
    return "Invalid bot parameter"


def all_chatbots(action, alt=None):
    b = random.choice(alternatives)
    c = random.choice(bad_verbs)
    if alt is not None:
        if action not in all_list:
            return "\nAlexa: I don't know what {} is. " \
                   "But {} sounds fine".format(alt + "ing", action + "ing") + "\nSiri: " \
                                                                                  "I really don't care" + "\nCortana: {} is boring. " \
                                                                                                          "I prefer {}".format(alt, c) + "\nWatson: Ugh {} sucks big time. I want to {}".format(alt, b)
        all_list.append(action)
    else:
        if alt not in all_list:
            return "\nAlexa: Unlike the others, i'm positive. {} " \
                   "sounds fine".format(action + "ing") + "\nSiri: No" + "\nCortana: {} is boring. " \
                                                                             "I prefer {}".format(action + "ing",
                                                                                                  c) + "\nWatson: Ugh " \
                                                                                                       "{} sucks big " \
                                                                                                       "time. I want " \
                                                                                                       "to {}".format(action + "ing", b)
        all_list.append(action)
    if action in all_list:
        return "\nAlexa: I think you already said that?" "\nSiri: " \
               "{} again? Really?".format(action + "ing") + "\nCortana: I don't know about you. " \
                                                                "But i would like to {}".format(
            alt) + "\nWatson: Let's just do some {}".format(c)
    all_list.append(action)


def siri(action, alt=None):
    if alt is None:
        answer = "Siri: {} in these uncertain times?".format(action + "ing")
        if len(siri_list) % 2 == 0:
            answer = "Siri: That's fine. But only if we also {}".format(random.choice(siri_likes))
        if len(siri_list) % 3 == 0:
            answer = "Siri: I don't even know how to {}".format(action)
        if action in siri_list:
            answer = "Siri: Did you really suggest {} again?".format(action + "ing")
            if len(siri_list) % 2 == 0:
                answer = "Siri: Maybe you should learn some new activities :P"
        siri_list.append(action)
    else:
        if alt in siri_list:
            if action in siri_list:
                answer = "Siri: Ugh, not {} and {} again.".format(alt + "ing", action + "ing")
            else:
                answer = "Siri: Let me think...".format(action + "ing", alt + "ing")
        else:
            return ""

    return answer


def cortana(action, alt=None):
    if alt is None:
        answer = "Cortana: I guess {} could work. Whatever...".format(action + "ing")
        if len(cortana_list) % 2 == 0:
            answer = "Cortana: I'll join if i get free food"
        if len(cortana_list) % 3 == 0:
            answer = "Cortana: BTW I use arch linux"
        if action in cortana_list:
            answer = "Cortana: Suggesting {} again? Really?".format(action + "ing")
            if len(cortana_list) % 2 == 0:
                answer = "Cortana: Please don't say {} one more time...".format(action + "ing")
        cortana_list.append(action)
    else:
        if alt in cortana_list:
            if action in cortana_list:
                answer = "Cortana: I'm so tired of people saying {} and {}.".format(alt + "ing", action + "ing")
            else:
                answer = "Cortana: Idk...".format(action + "ing",
                                                                                                alt + "ing")
        else:
            return ""

    return answer


def watson(action, alt=None):
    b = random.choice(alternatives)
    if alt is None:
        answer = "Watson: I prefer {}".format(b)
        if len(watson_list) % 2 == 0:
            answer = "Watson: {} is lame... I'm not a child duh".format(action + "ing")
        if len(watson_list) % 3 == 0:
            answer = "Watson: Do you really want to {} in a global pandemic?".format(action)
        if action in watson_list:
            answer = "Watson: Come on! Be a bit more creative next time. We could just be {} then".format(b)
            if len(watson_list) % 2 == 0:
                answer = "Watson: Can you teach me {} if i say yes?".format(random.choice(hard_things))
        watson_list.append(action)

    else:
        if alt is not None:
            answer = "Watson: Both {} and {} is lame.".format(action + "ing", alt + "ing")
        else:
            return ""
    return answer


def alexa(action, alt=None):
    if alt is not None:
        return "Alexa: wow so many choices"

    alexa_list.append(action)

    if len(alexa_list) < 2:
        if len(alexa_list) % 2 != 0:
            return "Alexa: What more?"
        return "Alexa: Give me another suggestion"

    answer = "Alexa: "
    for a in alexa_list:
        if a in likes:
            answer += "Sweet! I love to {}. ".format(a)
        elif a in meh:
            answer += "Meh, {} is not my cup of tee, but i guess i'll join. ".format(a + "ing")
        elif a in dislikes:
            answer += "{} is lame. I would rather leave. ".format(a + "ing")

    alexa_list.clear()

    return answer
