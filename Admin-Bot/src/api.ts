const BASE_URL = 'http://127.0.0.1:8000';

export default {
  async getCount() {
    try {
      const response = await fetch(`${BASE_URL}/bots/count/`);
      const data = await response.json();

      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async forward(start: number, end: number, message: string) {
    try {
      const response = await fetch(`${BASE_URL}/bots/sendMessage/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start, end,message }),
      });

      console.log('start:', start, ', last: ', end, 'id:', message);
      const data = await response.json();
      console.log(data);
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async stop_sending() {
    try {
      const response = await fetch(`${BASE_URL}/bots/stopSending/`);
      
      return "Done";
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async joinGroup(link:string) {
    try {
      const response = await fetch(`${BASE_URL}/groups/join/all`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({link}),
      });
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async joinGroupList(link:string) {
    try {
      const response = await fetch(`${BASE_URL}/groups/join/all/list/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({link}),
      });
      const data = await response.json();
      
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async getGroups() {
    try {
      const response = await fetch(`${BASE_URL}/groups/get_groups`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async getSenderSettings() {
    try {
      const response = await fetch(`${BASE_URL}/bots/settings/`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async changeSenderSettings(workingBotsAtSameTime: number, botMaxMessages: number) {
    try {
      const response = await fetch(`${BASE_URL}/bots/settings/change`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ workingBotsAtSameTime, botMaxMessages }),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

  async deleteGroup(id:string) {
    try {
      const response = await fetch(`${BASE_URL}/groups/deleteGroup?id=${id}`);
      const data = await response.json();
      console.log(data)
      return data;
    } catch (error) {
      console.error('Error:', error);
      return error;
    }
  },

};
