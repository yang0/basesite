BEGIN;
--
-- Create model MedicalOperator
--
CREATE TABLE `medicaloperator` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `uuid` varchar(32) NOT NULL comment 'uuid' , `title` varchar(100) NOT NULL comment '企业名称' , `mobile` varchar(20) NOT NULL comment '管理员手机号' , `enterprise_id` integer NOT NULL comment '基础库关联企业' , `create_time` datetime(6) NOT NULL comment '创建时间' , `update_time` datetime(6) NOT NULL comment '更新时间' , `owner_id` integer NOT NULL comment '企业管理员' );
ALTER TABLE `medicaloperator` ADD CONSTRAINT `medicaloperator_owner_id_5cd71590_fk_user_id` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`);
alter table medicaloperator comment '药品运营商';
COMMIT;
