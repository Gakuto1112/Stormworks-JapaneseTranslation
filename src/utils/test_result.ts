/**
 * テストでの指摘理由コード
 */
export const ReasonCode = {
    USED_PROHIBITED_CHARS: 1, /** 禁止文字を使用している */
    MISSING_TRANSLATION: 2 /** 翻訳が抜けている */
} as const;

/**
 * テストでの指摘理由を示す列挙型
 */
export type Reasons = typeof ReasonCode[keyof typeof ReasonCode];

/**
 * テスト結果を示すデータ型
 */
export interface TestResult {
    /** テストに合格したかどうか */
    passed: boolean,
    
    /** テストでの指摘点 */
    points: TestPoint[]
}

/**
 * テストでの指摘点テストでの指摘点を示すデータ型
 */
export interface TestPoint {
    /** 行番号 */
    line: number,
    
    /** 指摘理由 */
    reason: Reasons
}