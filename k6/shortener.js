
import http from 'k6/http';
import { check } from 'k6';
import { expectedStatuses, setResponseCallback } from 'k6/http';

setResponseCallback(expectedStatuses(201, 302));

export const options = {
  scenarios: {
    redirects: {
      executor: 'constant-arrival-rate',
      exec: 'get',
      rate: 3000,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 100,
      maxVUs: 500,
      tags: { endpoint: 'get' },
    },
    create_urls: {
      executor: 'constant-arrival-rate',
      exec: 'post',
      rate: 3000,
      timeUnit: '1s',
      duration: '60s',
      preAllocatedVUs: 100,
      maxVUs: 500,
      tags: { endpoint: 'post' },
    },
  },
  thresholds: {
    'http_req_failed{endpoint:get}': ['rate<0.01'],
    'http_req_failed{endpoint:post}': ['rate<0.01'],
    'checks{endpoint:get}': ['rate>0.99'],
    'checks{endpoint:post}': ['rate>0.99'],
    'http_req_duration{endpoint:get}': ['p(95)<50'],
    'http_req_duration{endpoint:post}': ['p(95)<50'],
  },
  summaryTrendStats: [
    'avg', 'min', 'med', 'p(90)', 'p(95)', 'p(99)', 'max',
  ],
};

const BASE_URL = __ENV.BASE_URL || 'http://app:8000';
const CODE = __ENV.CODE;

export function get() {
  const res = http.get(`${BASE_URL}/${CODE}`, {
    redirects: 0,
  });

  check(res, {
    'status is 302': (r) => r.status === 302,
    'has Location header': (r) => !!r.headers.Location,
  });
}

export function post() {
  const url = `https://example.com/test/${__VU}/${__ITER}/${Date.now()}`;

  const response = http.post(
    `${BASE_URL}/api/v1/urls`,
    JSON.stringify({ url }),
    {
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: '10s',
    },
  );

  check(response, {
    'status is 201': (r) => r.status === 201,
    'has short_code': (r) =>
      r.status === 201 && typeof r.json('short_code') === 'string',
    'has short_url': (r) =>
      r.status === 201 && typeof r.json('short_url') === 'string',
  });

  if (response.status !== 201) {
    console.error(
      `POST failed: ${response.status} ${response.body}`
    );
  }
}
