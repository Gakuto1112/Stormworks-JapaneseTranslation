import { error } from "../utils/logger";
import { ReasonCode } from "../utils/test_result";
import { TestBase } from "./test_base";

/**
 * テスト2を行うクラス
 * 
 * **** テスト2 ****
 * 日本語訳の追加し忘れをチェックする。
 * 英語も空白の場合は日本語が空白でも無視する。
 */
class Test2 extends TestBase {
    /**
     * テスト実行時に各翻訳キーに対して実行する関数
     * @param line 翻訳ファイルの行番号
     * @param id コンポーネントID。コンポーネントに関する翻訳キー以外は空文字になる。
     * @param en 英語原文。翻訳ファイルが不完全だとundefinedになっていることもある。
     * @param local 日本訳文。翻訳ファイルが不完全だとundefinedになっていることもある。
     */
    protected testFunction(line: number, _id: string, en?: string | undefined, local?: string | undefined): void {
        if(en != undefined) {
            if(en.length > 0 && (local == undefined || local.length == 0)) {
                error(line, `Cannot find local string at line ${line}.`);
                this.testResult.passed = false;
                this.testResult.points.push({line: line, reason: ReasonCode.MISSING_TRANSLATION});
            }
        }
    }
}

async function test2(): Promise<void> {
    console.info("Checking local strings...");

    const tester: Test2 = new Test2();
    const testPassed: boolean = await tester.run();
    tester.exportTestResult();
    
    if(testPassed) {
        console.info("Finished checking local strings. No missing line detected.");
        process.exit(0);
    }
    else {
        console.error("One or more lines are missing their local strings! Please add local strings.");
        process.exit(1);
    }
}

test2();
