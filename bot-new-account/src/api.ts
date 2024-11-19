const BASE_URL = 'http://127.0.0.1:8000';

export default {
  async sendCode(phone: string) {
    try {
      const response = await fetch(`${BASE_URL}/auth/send-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone }),
      });
      const data = await response.json();
      console.log('data:', data);
      return data;
    } catch (error: any) {
      console.error('Error:', error);
      return error;
    }
  },

  async verifyCode(phone: string, code: string, phone_code_hash: string) {
    try {
      const response = await fetch(`${BASE_URL}/auth/verify-code`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, code,phone_code_hash }),
      });
      const data = await response.json();
      console.log(data);

      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },
};
