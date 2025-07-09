/**
 * 標準出力に警告メッセージを出力する。
 * @param line 翻訳データの行番号
 * @param message 警告メッセージ
 */
export function warn(line: number, message: string): void {
    console.warn(`[Warning : ${line}]: ${message}`);
}

/**
 * 標準出力にエラーメッセージを出力する。
 * これを呼び出したからといってプログラムがエラー終了することはない。
 * @param line 翻訳データの行番号
 * @param message エラーメッセージ
 */
export function error(line: number, message: string): void {
    console.error(`[Error : ${line}]: ${message}`);
}
