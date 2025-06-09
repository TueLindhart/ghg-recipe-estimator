// loader just forwards the :jobId param
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => ({ jobId: params.jobId });
