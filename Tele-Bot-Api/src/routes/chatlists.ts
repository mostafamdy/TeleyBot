import { joinChatlist } from '@/controllers/chatlists';
import { Router } from 'express';

const chatlistRouter = Router();

chatlistRouter.get('/join', joinChatlist);

export default chatlistRouter;
