import { Router } from 'express';
import authRouter from './auth';
import botsRouter from './bots';
import chatlistRouter from './chatlists';
import messagesRouter from './messages';

const apiRouter = Router();

apiRouter.use('/auth', authRouter);
apiRouter.use('/bots', botsRouter);
apiRouter.use('/messages', messagesRouter);
apiRouter.use('/chatlists', chatlistRouter);

export default apiRouter;
