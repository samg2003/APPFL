from .server_federated_pca import FedServerPCA
import torch


class ServerFedAdagradPCA(FedServerPCA):
    def compute_step(self):

        super(ServerFedAdagradPCA, self).compute_pseudo_gradient()

        super(ServerFedAdagradPCA, self).update_m_vector()
        
        self.v_vector = self.v_vector + torch.square(self.pseudo_grad)

        temp = torch.div(self.server_learning_rate*self.m_vector, torch.sqrt(self.v_vector) + self.server_adapt_param)
        
        self.step = - torch.mm( self.P.transpose(0, 1), temp.reshape(-1,1))
                
         

    def logging_summary(self, cfg, logger):
        super(FedServerPCA, self).log_summary(cfg, logger)

        logger.info("client_learning_rate = %s " % (cfg.fed.args.optim_args.lr))
        logger.info(
            "server_momentum_param_1 = %s " % (cfg.fed.args.server_momentum_param_1)
        )

        logger.info("server_adapt_param = %s " % (cfg.fed.args.server_adapt_param))
        logger.info("server_learning_rate = %s " % (cfg.fed.args.server_learning_rate))
        logger.info(
            "server_momentum_param_2 = %s " % (cfg.fed.args.server_momentum_param_2)
        )

        if cfg.summary_file != "":
            with open(cfg.summary_file, "a") as f:

                f.write(
                    cfg.logginginfo.DataSet_name
                    + " FedAdagrad ClientLR "
                    + str(cfg.fed.args.optim_args.lr)
                    + " MParam1 "
                    + str(cfg.fed.args.server_momentum_param_1)
                    + " AdaptParam "
                    + str(cfg.fed.args.server_adapt_param)
                    + " ServerLR "
                    + str(cfg.fed.args.server_learning_rate)
                    + " MParam2 "
                    + str(cfg.fed.args.server_momentum_param_2)
                    + " TestAccuracy "
                    + str(cfg.logginginfo.accuracy)
                    + " BestAccuracy "
                    + str(cfg.logginginfo.BestAccuracy)
                    + " Time "
                    + str(round(cfg.logginginfo.Elapsed_time, 2))
                    + "\n"
                )