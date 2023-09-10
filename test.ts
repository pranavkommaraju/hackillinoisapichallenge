const axios = require('axios');

const BASE_URL = 'http://127.0.0.1:5000/';

describe('API Endpoints', () => {
  it('should encode and decode data', async () => {
    const data = {
      user: 'john_doe',
      data: {
        role: 'admin',
        access_level: 5,
      }
    };

    const encodeResponse = await axios.post(`${BASE_URL}/encode`, data);

    expect(encodeResponse.status).toBe(200);

    const encodedToken = encodeResponse.data.token;

    const decodeResponse = await axios.post(`${BASE_URL}/decode`, {
      token: encodedToken,
    });

    expect(decodeResponse.status).toBe(200);

    const decodedData = decodeResponse.data;

    expect(decodedData).toEqual(data);
  });
});
