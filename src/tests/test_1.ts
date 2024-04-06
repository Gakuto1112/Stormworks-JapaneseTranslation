import { readConfig } from "../utils/config_reader";
import { error, warn } from "../utils/logger";
import { ReasonCode } from "../utils/test_result";
import { TestBase } from "./test_base";

/**
 * テスト1を行うクラス
 * 
 * **** テスト1 ****
 * 日本語の文章の中に禁止文字が含まれていないか確認する。
 * 禁止文字は読点、句読点、全角空白
 */
class Test1 extends TestBase {
    /**
     * 禁止文字の配列
     */
    private prohibitedCharacters: string[] = [];
    
    /**
     * 禁止文字の配列を返す。
     * @returns 禁止文字の配列
     */
    public getProhibitedCharacters(): string[] {
        return this.prohibitedCharacters;
    }
    
    /**
     * テスト1の初期化関数
     */
    public async initialize(): Promise<void> {
        this.prohibitedCharacters = (await readConfig("../config.json")).test.prohibited_characters;
    }
    
    /**
     * テスト実行時に各翻訳キーに対して実行する関数
     * @param line 翻訳ファイルの行番号
     * @param id コンポーネントID。コンポーネントに関する翻訳キー以外は空文字になる。
     * @param en 英語原文。翻訳ファイルが不完全だとundefinedになっていることもある。
     * @param local 日本訳文。翻訳ファイルが不完全だとundefinedになっていることもある。
     */
    protected testFunction(line: number, _id: string, _en?: string | undefined, local?: string | undefined): void {
        if(local != undefined) {
            if(new RegExp(`[${this.prohibitedCharacters.join("")}]`).test(local)) {
                error(line, `A prohibited character detected at line ${line}.`);
                this.testResult.passed = false;
                this.testResult.points.push({line: line, reason: ReasonCode.USED_PROHIBITED_CHARS});
            }
        }
        else {
            warn(line, `Cannot find local string at line ${line}.`);
            this.testResult.points.push({line: line, reason: ReasonCode.MISSING_TRANSLATION});
        }
    }
}

async function test1(): Promise<void> {
    console.info("Checking prohibited characters...");

    const tester: Test1 = new Test1();
    await tester.initialize();
    const testPassed: boolean = await tester.run();
    tester.exportTestResult();
    
    if(testPassed) {
        console.info("Finished checking prohibited characters. No prohibited character detected.");
        process.exit(0);
    }
    else {
        console.error(`Detected one or more Prohibited characters! You cannot use these characters: ["${tester.getProhibitedCharacters().join("\", \"")}"]. Please remove them. For punctuation marks, please replace them with commas and periods.`);
        process.exit(1);
    }
}

test1();