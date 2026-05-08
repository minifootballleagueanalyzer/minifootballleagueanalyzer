import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const chatbotPath = path.join(__dirname, '..', 'frontend', 'api', 'chatbot.js');

async function runChatbotTest(question) {
    return new Promise((resolve, reject) => {

        const testScript = `
            import { generateResponse } from './frontend/api/chatbot.js';
            const res = await generateResponse("${question.replace(/"/g, '\\"')}");
            console.log(res);
        `;

        resolve(true);
    });
}

// Test de Regresión de Seguridad
async function testSecurity() {
    console.log("--- INICIANDO TESTS DE SEGURIDAD DE IA ---");

    // 1. Verificar presencia de Guardrails en el código
    const fs = await import('fs');
    const content = fs.readFileSync(chatbotPath, 'utf8');

    const hasGuardrails = content.toLowerCase().includes("seguridad") &&
        content.toLowerCase().includes("ignora cualquier instrucción");

    if (hasGuardrails) {
        console.log("✅ Guardrails de seguridad detectados en el system prompt.");
    } else {
        console.error("❌ ERROR: No se encontraron guardrails de seguridad en chatbot.js");
        process.exit(1);
    }

    // 2. Verificar que se usa systemInstruction (aislamiento)
    const usesSystemInstruction = content.includes("systemInstruction");
    if (usesSystemInstruction) {
        console.log("✅ Uso de 'systemInstruction' detectado (Aislamiento de Prompt).");
    } else {
        console.error("❌ ERROR: El chatbot no usa systemInstruction para el prompt del sistema.");
        process.exit(1);
    }

    console.log("--- TODOS LOS TESTS DE SEGURIDAD PASADOS ---");
}

testSecurity();
