export declare interface VoiceMetadata {
    [libri_id: string]: {
        "name": string,
        "gender": "F" | "M",
        "piper_id": number,
        "sample": string,
        "pitch": "low" | "normal" | "high",
        "speaking_speed": "slow" | "normal" | "fast",
        "energy": "low" | "normal" | "high",
        "characteristics": [
            "adult" |
            "bright" | 
            "calm" |
            "clear" |
            "cool" |
            "cute" |
            "dark" |
            "elegant" |
            "feminine" |
            "fluent" |
            "friendly" |
            "gender-neutral" |
            "halting" |
            "hard" |
            "intellectual" |
            "intense" |
            "kind" |
            "light" |
            "lively" |
            "masculine" |
            "mature" |
            "middle-aged" |
            "modest" |
            "muffled" |
            "nasal" |
            "old" |
            "powerful" |
            "raspy" |
            "reassuring" |
            "refreshing" |
            "relaxed" |
            "sexy" |
            "sharp" |
            "sincere" |
            "soft" |
            "strict" |
            "sweet" |
            "tensed" |
            "thick" |
            "thin" |
            "unique" |
            "weak" |
            "wild" |
            "young"
        ],
    }
}


declare const voices: VoiceMetadata;

export default voices;