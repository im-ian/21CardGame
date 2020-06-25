import os
import random
import time

# 게임에 사용되는 변수들을 정의합니다.
player = {
    "hand": [],
    "score": 0,
}

computer = {
    "hand": [],
    "score": 0,
}

cardList = [
    {"icon": "🂡", "name": "카드 1", "value": 1},
    {"icon": "🂢", "name": "카드 2", "value": 2},
    {"icon": "🂣", "name": "카드 3", "value": 3},
    {"icon": "🂤", "name": "카드 4", "value": 4},
    {"icon": "🂥", "name": "카드 5", "value": 5},
    {"icon": "🂦", "name": "카드 6", "value": 6},
    {"icon": "🂧", "name": "카드 7", "value": 7},
    {"icon": "🂨", "name": "카드 8", "value": 8},
    {"icon": "🂩", "name": "카드 9", "value": 9},
    {"icon": "🂪", "name": "카드 10", "value": 10},
    {"icon": "🃟", "name": "카드 11", "value": 11},
]

blindCard = "🂠"


def main():
    isExit = False

    while True:
        try:
            clearConsole()
            # 게임 메뉴입니다.
            print("\n[블랙잭]\n")
            print("서로 번갈아면서 무작위의 카드를 받아 숫자의 합이 최대한 21과 가깝게 만드는 게임입니다.\n")
            print("1. 카드의 합이 21을 초과하면 패배합니다.")
            print("2. 양쪽의 플레이어가 21을 초과하면 21에 가장 근접한 플레이어가 승리합니다.")
            print("3. 같은 숫자의 카드는 한 장씩만 존재합니다.")
            print("4. 양쪽의 플레이어가 모두 카드를 받지 않으면 결과를 확인합니다.")
            print("5. 서로의 두 번째 카드는 까지는 공개됩니다.\n ")
            gameMenu = int(input("[1] 게임 시작 [2] 종료 \n>> "))
            if gameMenu == 1:
                break
            elif gameMenu == 2:
                isExit = True
                break
        except:
            # input 값을 int 변환에 실패하면 except로 오류를 처리합니다.
            print("\n[오류] 정상적이지 못한 값을 입력받았습니다.")
            time.sleep(1)

    if isExit:
        return

    clearConsole()

    # 기본적으로 2장의 카드를 가지고 시작합니다.
    for i in range(0, 2):
        drawPlayer()
        drawComputer()

    while True:
        print("행동을 선택하세요.")
        print("양쪽의 플레이어가 카드를 받지 않으면 결과를 확인합니다.\n")

        print("상대\t", end="")
        cardCount = 0
        for i in computer["hand"]:
            # 카드를 2장까지 공개합니다.
            if cardCount <= 1:
                print("%s %-4s" % (i["icon"], i["value"]), end="")
            else:
                print("%s %-4s" % (blindCard, "?"), end="")

            cardCount += 1

        print("\n나\t", end="")
        for i in player["hand"]:
            print("%s %-4s" % (i["icon"], i["value"]), end="")

        try:
            action = int(input("\n\n[1] 카드 받기 [2] 그만 받기 \n>> "))
            print("")

            if action == 1:
                # 플레이어 카드 뽑기
                drawPlayer()
                print("[안내] 카드를 받았습니다.")

                time.sleep(1)

                # 컴퓨터 카드 뽑기 처리
                if potodds():
                    drawComputer()
                    print("[안내] 상대방이 카드를 받습니다.\n")
                else:
                    print("[안내] 상대방은 카드를 받지 않았습니다.\n")

                time.sleep(1)

                print("%s" % "=" * 20, end="\n\n")
                continue
            elif action == 2:
                # 컴퓨터도 그만 받는지 확인
                if potodds():
                    print("[안내] 카드를 받지 않았습니다.")
                    time.sleep(1)

                    drawComputer()
                    print("[안내] 상대방이 카드를 받습니다.\n")
                    time.sleep(1)
                    print("%s" % "=" * 20, end="\n\n")
                    continue
                else:
                    break
        except:
            continue

    print("%s" % "=" * 20, end="\n\n")
    print("[안내] 게임 승부 결과입니다.\n")
    print("상대\t", end="")
    for i in computer["hand"]:
        print("%s %-4s" % (i["icon"], i["value"]), end="")

    print("= %d" % computer["score"], end="\n")

    print("나\t", end="")
    for i in player["hand"]:
        print("%s %-4s" % (i["icon"], i["value"]), end="")

    print("= %d" % player["score"], end="\n\n")

    # 두 플레이어 모두 21을 초과한 경우
    if player["score"] == computer["score"]:
        # 플레이어와 컴퓨터의 점수가 같을 경우
        print("무승부입니다.")
    elif player["score"] > 21 and computer["score"] > 21:
        # 플레이어와 컴퓨터 모두 21을 초과한 경우 가장 근접한 사람이 승리
        if player["score"] < computer["score"]:
            print("플레이어가 승리했습니다!")
        else:
            print("상대방이 승리했습니다!")
    elif player["score"] == 21 and computer["score"] != 21:
        # 플레이어가 21을 만들었을 경우
        print("플레이어가 승리했습니다!")
    elif player["score"] != 21 and computer["score"] == 21:
        # 컴퓨터가 21을 만들었을 경우
        print("상대방이 승리했습니다!")
    elif player["score"] < 21 and computer["score"] > 21:
        # 컴퓨터만 21을 초과한 경우
        print("플레이어가 승리했습니다!")
    elif player["score"] > 21 and computer["score"] < 21:
        # 플레이어만 21을 초과한 경우
        print("상대방이 승리했습니다!")
    elif player["score"] > computer["score"]:
        # 컴퓨터보다 플레이어 점수가 높을 때
        print("플레이어가 승리했습니다!")
    elif player["score"] < computer["score"]:
        # 플레이어보다 컴퓨터 점수가 높을 때
        print("상대방이 승리했습니다!")
    else:
        print("승리 조건 미지정")


def clearConsole():
    os.system("cls" if os.name == "nt" else "clear")


def drawRandomCard():
    cardIndex = random.randint(0, len(cardList) - 1)
    cardInfo = cardList[cardIndex]
    del cardList[cardIndex]
    return cardInfo


def drawPlayer():
    card = drawRandomCard()
    player["hand"].append(card)
    player["score"] += card["value"]


def drawComputer():
    card = drawRandomCard()
    computer["hand"].append(card)
    computer["score"] += card["value"]


# 컴퓨터가 카드를 받을지의 여부를 결정하는 알고리즘입니다.
def potodds():
    if (computer["score"] >= 21):
        # 21점이거나 21점이 넘어가면 그만 받음.
        return False
    else:
        # 컴퓨터가 뽑아야 하는 숫자
        need = 21 - computer["score"]
        # 뽑아야 하는 수가 11보다 크다면
        if need > 11:
            return True

        # 내 카드 숫자들을 list로 만듬
        computerHand = list(map(lambda v: v["value"], computer['hand']))
        # 나의 공개된 카드
        openPlayerHand = [player["hand"][0]["value"], player["hand"][1]["value"]]

        if need in openPlayerHand:
            # 만약 뽑으려는 카드가 상대 수중에 있을 경우.
            if computer["score"] <= 17 and computer["score"] >= 18:
                # 50% 확률로 뽑음
                return random.randint(0, 2) == 0
            elif computer["score"] <= 19 and computer["score"] >= 20:
                # 1 혹은 2를 상대가 가지고 있음으로 그만 뽑음.
                return False
            else:
                return True
        else:
            # 만약 뽑으려는 카드가 상대 수중에 없다고 가정할 경우.
            # 내 손에 뽑으려는 카드가 있으면 그 보다 작은 수가 있는지 확인
            underCase = 0
            for v in range(1, need):
                if v in computerHand or v in openPlayerHand:
                    continue
                underCase += 1

            return random.randint(1, len(cardList)) <= underCase



if __name__ == "__main__":
    main()
