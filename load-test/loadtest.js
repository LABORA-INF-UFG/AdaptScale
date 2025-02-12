import http from 'k6/http';
import { sleep } from 'k6';
import { check } from 'k6';

// Função para criar os estágios de carga com ramp-up e ramp-down controlados
function createLoadStages() {
    let stages = [];
    const normalUserMin = 55; // Usuários em carga normal
    const normalUserMax = 65;
    const peakUserMax = 700; // Pico máximo de usuários
    const totalTestDuration = 122; // Tempo total: 122 minutos
    const peakDuration = 10; // Pico: 10 minutos
    const rampDuration = 5; // Ramp-up e ramp-down: 5 minutos
    const numPeaks = 2; // Número de picos

    // Tempo total dedicado a picos e ramps
    const timeForPeaks = numPeaks * (peakDuration + 2 * rampDuration);
    const remainingTimeForNormalLoad = totalTestDuration - timeForPeaks;
    const normalLoadDuration = Math.floor(remainingTimeForNormalLoad / (numPeaks + 1));

    // Carga normal inicial
    for (let i = 0; i < normalLoadDuration; i++) {
        let normalUsers = Math.floor(Math.random() * (normalUserMax - normalUserMin + 1)) + normalUserMin;
        stages.push({ duration: '1m', target: normalUsers });
    }

    // Carga regular + picos de sobrecarga
    for (let i = 0; i < numPeaks; i++) {
        // Ramp-up gradual
        for (let j = 1; j <= rampDuration; j++) {
            stages.push({ duration: '1m', target: Math.floor((peakUserMax / rampDuration) * j) });
        }

        // Pico estabilizado
        for (let j = 0; j < peakDuration; j++) {
            stages.push({ duration: '1m', target: peakUserMax });
        }

        // Ramp-down gradual
        for (let j = rampDuration; j > 0; j--) {
            stages.push({ duration: '1m', target: Math.floor((peakUserMax / rampDuration) * j) });
        }

        // Carga normal entre picos (exceto após o último pico)
        if (i < numPeaks - 1) {
            for (let j = 0; j < normalLoadDuration; j++) {
                let normalUsers = Math.floor(Math.random() * (normalUserMax - normalUserMin + 1)) + normalUserMin;
                stages.push({ duration: '1m', target: normalUsers });
            }
        }
    }

    // Carga normal final após o último pico
    for (let i = 0; i < normalLoadDuration; i++) {
        let normalUsers = Math.floor(Math.random() * (normalUserMax - normalUserMin + 1)) + normalUserMin;
        stages.push({ duration: '1m', target: normalUsers });
    }

    return stages;
}

// Configuração do teste
export let options = {
    stages: createLoadStages(),
    thresholds: {
        http_req_duration: ['p(95)<400'], // 95% das requisições com tempo < 400ms
        http_req_failed: ['rate<0.01'],   // Falha < 1%
        checks: ['rate>0.99'],           // Sucesso > 99%
    },
};

export default function () {
    let res = http.get('https://virtualhubs.online');

    let success = check(res, {
        'status code is 2xx': (r) => r.status >= 200 && r.status < 300,
        'response time < 400ms': (r) => r.timings.duration < 400,
    });

    if (!success) {
        console.error(`Erro na requisição. Status: ${res.status}, Duração: ${res.timings.duration}ms`);
    }

    sleep(Math.random() * 2.5 + 0.5); // Entre 0,5s e 3s
}

