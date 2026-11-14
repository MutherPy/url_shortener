
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    redirects: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 50,
      maxVUs: 200,
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<50'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://host.docker.internal:8000';
const CODE = __ENV.CODE;

export default function () {
  const res = http.get(`${BASE_URL}/${CODE}`, {
    redirects: 0,
  });

  check(res, {
    'status is 302': (r) => r.status === 302,
    'has Location header': (r) => !!r.headers.Location,
  });
}
