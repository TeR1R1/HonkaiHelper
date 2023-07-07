 aocr.gameOCR(
        np.array(aocr.getScreenshot(honkai3))
    )
    
    inst = [
        ['补给', (0, 0, GAME_WIDTH, GAME_HEIGHT)],
        ['前往商店', (0, 0, GAME_WIDTH, GAME_HEIGHT)]
    ]
    touch(
        (1109, 476)
    )
    doInst(ins