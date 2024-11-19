import { saveMessage } from '@/controllers/messages';
import { Router } from 'express';

const messagesRouter = Router();

messagesRouter.post('/save', saveMessage);

export default messagesRouter;
