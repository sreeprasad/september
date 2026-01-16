import { GoogleGenAI } from "@google/genai";
import { BriefingRequest, BriefingResponse } from "../types";

const apiKey = process.env.API_KEY || '';

// Initialize the client once
const ai = new GoogleGenAI({ apiKey });

export const generateBriefing = async (request: BriefingRequest): Promise<BriefingResponse> => {
  if (!apiKey) {
    throw new Error("API Key is missing. Please check your configuration.");
  }

  const { profileUrl, twitterHandle, context } = request;

  const prompt = `
    I need a comprehensive meeting briefing for a ${context}.
    
    Target Profile: ${profileUrl}
    ${twitterHandle ? `Twitter Handle: ${twitterHandle}` : ''}
    
    Please perform a deep search on this person/company. 
    
    Structure the response in Markdown with the following sections:
    1. **Executive Summary**: Who they are, current role, key achievements (2-3 sentences).
    2. **Ice Breakers**: 3 personalized conversation starters based on recent news, posts, or shared interests.
    3. **Professional Trajectory**: Summary of their career path and recent moves.
    4. **Meeting Strategy**: Specific advice for a ${context} based on their background.
    5. **Red Flags / Topics to Avoid**: (If any found, otherwise omit).
    
    Keep the tone professional, insightful, and strategic.
  `;

  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: prompt,
      config: {
        tools: [{ googleSearch: {} }], // Use Google Search for real-time intel
        systemInstruction: "You are an elite executive assistant and intelligence analyst. Your goal is to prepare the user to master their upcoming meeting.",
      }
    });

    const markdown = response.text || "No content generated.";
    
    // Extract sources if available
    const chunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
    const sources = chunks
      .filter((c: any) => c.web?.uri && c.web?.title)
      .map((c: any) => ({
        title: c.web.title,
        uri: c.web.uri
      }));

    return {
      markdown,
      sources: sources.length > 0 ? sources : undefined
    };

  } catch (error) {
    console.error("Gemini API Error:", error);
    throw new Error("Failed to generate briefing. Please try again.");
  }
};
