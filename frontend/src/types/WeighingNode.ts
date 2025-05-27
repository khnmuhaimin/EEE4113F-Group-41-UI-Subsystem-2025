export type WeighingNode = {
    id: string;
    location: string | null;
    registration_in_progress: boolean;
    leds_flashing: boolean;
    last_pinged_at: string;
    created_at: string; // ISO datetime string
};