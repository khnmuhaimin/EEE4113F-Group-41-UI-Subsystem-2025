export type WeighingNode = {
    id: string;
    location: string | null;
    registration_in_progress: boolean;
    leds_flashing: boolean;
    created_at: string; // ISO datetime string
};