export type ProcessResponse = {
  status: boolean;
  message: string;
  data: {
    result: {
      bicycle: number;
      car: number;
      bus: number;
      motorbike: number;
      person: number;
      truck: number;
    };
    result_url: string;
    upload_url: string;
  } | null;
};
