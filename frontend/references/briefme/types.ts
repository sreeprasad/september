export interface BriefingRequest {
  profileUrl: string;
  twitterHandle?: string;
  context: string;
}

export interface BriefingResponse {
  markdown: string;
  sources?: Array<{
    title: string;
    uri: string;
  }>;
}

export enum MeetingContext {
  PARTNERSHIP = 'Partnership Meeting',
  SALES_DISCOVERY = 'Sales Discovery',
  JOB_INTERVIEW = 'Job Interview',
  INVESTOR_PITCH = 'Investor Pitch',
  NETWORKING = 'Casual Networking',
  MENTORSHIP = 'Mentorship Session'
}
