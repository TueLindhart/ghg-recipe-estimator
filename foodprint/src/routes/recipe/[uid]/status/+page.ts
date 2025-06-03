// loader just forwards the :uid param
import type { PageLoad } from './$types';

export const load: PageLoad = ({ params }) => ({ uid: params.uid });
