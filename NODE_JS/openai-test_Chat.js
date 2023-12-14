import OpenAI from "openai";

const openai = new OpenAI();

async function main() {
  const completion = await openai.chat.completions.create({
    messages: [{ role: "system", content: "This is a test message" }],
    model: "gpt-3.5-turbo",
  });

  //console.log(completion.choices[0]);
  console.log(completion.choices[0].message.content)
}

main();